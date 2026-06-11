import React, { useState } from "react";
import { predictSingle } from "../services/api";
import type { SinglePredictionResult } from "../types/prediction";

export default function TransactionForm() {
  const [txForm, setTxForm] = useState({ amount: '', nameOrig: '', oldBalanceOrg: '', newBalanceOrig: '', nameDest: '', oldBalanceDest: '', newBalanceDest: '', type: 'Transfer' });
  const [txMessage, setTxMessage] = useState<string | null>(null);
  const [singleResult, setSingleResult] = useState<SinglePredictionResult | null>(null);

  const handleTxChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setTxForm((s) => ({ ...s, [name]: value }));
  };

  const handleTxSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setTxMessage(null);
    setSingleResult(null);

    const payload = {
      amount: Number(txForm.amount) || 0,
      nameOrig: txForm.nameOrig,
      oldbalanceOrg: Number(txForm.oldBalanceOrg) || 0,
      newbalanceOrig: Number(txForm.newBalanceOrig) || 0,
      nameDest: txForm.nameDest,
      oldbalanceDest: Number(txForm.oldBalanceDest) || 0,
      newbalanceDest: Number(txForm.newBalanceDest) || 0,
      type: txForm.type,
    };

    try {
      setTxMessage('Sending to model...');
      const data = await predictSingle(payload);
      if (data && data.status === 'success') {
        setSingleResult(data.data as SinglePredictionResult);
        setTxMessage('Prediction received');
      } else {
        setTxMessage('Prediction failed');
      }
    } catch (err) {
      console.error('Single predict error', err);
      setTxMessage(err instanceof Error ? err.message : 'Request failed');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}>
      <form onSubmit={(e) => { e.preventDefault(); handleTxSubmit(); }} className="transaction-form" style={{ width: '100%', maxWidth: 900, background: '#000', color: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 6px 18px rgba(0,0,0,0.1)' }}>
        <h3 style={{ marginTop: 0, marginBottom: 16 }}>Transaction Input</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          <label style={{ display: 'block', color: '#fff' }}>
            Amount
            <input name="amount" value={txForm.amount} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
          </label>
          <label style={{ display: 'block', color: '#fff' }}>
            Transaction Type
            <select name="type" value={txForm.type} onChange={handleTxChange} style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }}>
              <option>Cash In</option>
              <option>Cash Out</option>
              <option>Transfer</option>
              <option>Debit</option>
              <option>Payment</option>
            </select>
          </label>

          <label style={{ display: 'block', color: '#fff' }}>
            Sender Name (nameOrig)
            <input name="nameOrig" value={txForm.nameOrig} onChange={handleTxChange} type="text" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
          </label>
          <label style={{ display: 'block', color: '#fff' }}>
            Receiver Name (nameDest)
            <input name="nameDest" value={txForm.nameDest} onChange={handleTxChange} type="text" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
          </label>

          <label style={{ display: 'block', color: '#fff' }}>
            Sender Old Balance (oldBalanceOrig)
            <input name="oldBalanceOrg" value={txForm.oldBalanceOrg} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
          </label>
          <label style={{ display: 'block', color: '#fff' }}>
            Sender New Balance (newBalanceOrig)
            <input name="newBalanceOrig" value={txForm.newBalanceOrig} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
          </label>

          <label style={{ display: 'block', color: '#fff' }}>
            Receiver Old Balance (oldBalanceDest)
            <input name="oldBalanceDest" value={txForm.oldBalanceDest} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
          </label>
          <label style={{ display: 'block', color: '#fff' }}>
            Receiver New Balance (newBalanceDest)
            <input name="newBalanceDest" value={txForm.newBalanceDest} onChange={handleTxChange} type="number" step="any" style={{ width: '100%', padding: 8, marginTop: 6, background: '#fff', color: '#000', border: '1px solid #ccc', borderRadius: 4 }} />
          </label>
        </div>

        <div style={{ marginTop: 16, display: 'flex', gap: 12 }}>
          <button type="submit" className="tx-submit">Enter</button>
          <button type="button" className="reset-button" onClick={() => { setTxForm({ amount: '', nameOrig: '', oldBalanceOrg: '', newBalanceOrig: '', nameDest: '', oldBalanceDest: '', newBalanceDest: '', type: 'Transfer' }); setTxMessage(null); }}>Reset</button>
          {txMessage && <div style={{ marginLeft: 12, alignSelf: 'center', color: '#4caf50' }}>{txMessage}</div>}
        </div>

        {singleResult && (
          <div style={{ marginTop: 16, background: '#fff', color: '#000', padding: 12, borderRadius: 8, maxWidth: 900 }}>
            <div style={{ fontWeight: 700 }}>Transaction Result</div>
            <div style={{ marginTop: 8 }}>Decision: <strong>{singleResult.final_decision}</strong></div>
            <div>Voting: {singleResult.voting_ratio}</div>
            <div style={{ marginTop: 8 }}>
              <div style={{ fontWeight: 600 }}>Model details:</div>
              <ul>
                {Array.isArray(singleResult.model_details) && singleResult.model_details.map((m: any, idx: number) => (
                  <li key={idx}>{m.model_name}: {m.is_fraud ? 'FRAUD' : 'SAFE'} ({m.confidence_score}%)</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}
