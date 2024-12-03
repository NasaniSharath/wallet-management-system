import React, { useState } from 'react';
import { getBalance, addMoney, transferMoney, getTransactions } from '../services/api'; // Import API functions
import 'bootstrap/dist/css/bootstrap.min.css';
import { handleDecrypt } from './encryptDecrypt';

const WalletDashboard = () => {
  // Define state variables
  const wid = handleDecrypt( localStorage.getItem("wallet_id"))
  const [walletId, setWalletId] = useState(wid);
  const [balance, setBalance] = useState(null);
  const [addAmount, setAddAmount] = useState('');
  const [fromWalletId, setFromWalletId] = useState(wid);
  const [toWalletId, setToWalletId] = useState('');
  const [transferAmount, setTransferAmount] = useState('');
  const [transactions, setTransactions] = useState([]);
  const [err_msg_transfer_money, setErrMsgTransferMoney] = useState('')

  // Handle balance check
  const handleCheckBalance = async () => {
    try {
      await getBalance(walletId).then((res)=>{
        if(res.status === 200){
          setBalance(res.data.balance);
        }
      }).catch((err)=>{
        console.log(err);
      })
      
    } catch (error) {
      alert(error.message || 'Error fetching balance');
    }
  };

  // Handle adding money
  const handleAddMoney = async () => {
    try {
      let payload = {
        "wallet_id":walletId, 
        "amount":parseFloat(addAmount)
      }
      await addMoney(payload).then((res)=>{
        if(res.status ===200){
          setBalance(res.updated_balance);
          alert('Money added successfully');
        }
      }).catch((error)=>{
        console.log(error)
      })
      
    } catch (error) {
      alert(error.message || 'Error adding money');
    }
  };

  // Handle transferring money
  const handleTransferMoney = async () => {
    try {
      let payload = {
        "from_wallet_id":fromWalletId,
        "to_wallet_id":toWalletId,
        "amount":parseFloat(transferAmount)
      }
      await transferMoney(payload).then((res)=>{
        if(res.status === 200){
        alert('Money transferred successfully');
        }
        else{
          console.log(res)
        setErrMsgTransferMoney('')
        }
      }).catch((err)=>{
        console.log("err:",err.response)
        setErrMsgTransferMoney(err.response.data.error)
      })
      
    } catch (error) {
      alert(error.message || 'Error transferring money');
    }
  };

  // Handle fetching transaction history
  const handleFetchTransactions = async () => {
    try {
      await getTransactions(walletId).then((res)=>{
        if(res.status ===200){
          setTransactions(res.data.data);
        }

      }).catch((err)=>{
        console.log(err)
      })
      
    } catch (error) {
      alert(error.message || 'Error fetching transactions');
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4 text-center">Wallet Dashboard</h2>

      {/* Check Balance */}
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Check Balance</h5>
          <div className="form-group">
            <input
              type="text"
              className="form-control"
              placeholder="Enter Wallet ID"
              value={walletId}
              onChange={(e) => setWalletId(e.target.value)}
              disabled
            />
          </div>
          <button className="btn btn-primary mt-2" onClick={handleCheckBalance}>
            Check Balance
          </button>
          {balance !== null && <h5 className="mt-3">Balance: {balance}</h5>}
        </div>
      </div>

      {/* Add Money */}
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Add Money</h5>
          <div className="form-group">
            <input
              type="number"
              className="form-control"
              placeholder="Enter Amount"
              value={addAmount}
              onChange={(e) => setAddAmount(e.target.value)}
            />
          </div>
          <button className="btn btn-success mt-2" onClick={handleAddMoney}>
            Add Money
          </button>
        </div>
      </div>

      {/* Transfer Money */}
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Transfer Money</h5>
          <div className="form-group">
            <input
              type="text"
              className="form-control mb-2"
              placeholder="From Wallet ID"
              value={fromWalletId}
              onChange={(e) => setFromWalletId(e.target.value)}
              disabled
            />
            <input
              type="text"
              className="form-control mb-2"
              placeholder="To Wallet ID"
              value={toWalletId}
              onChange={(e) => setToWalletId(e.target.value)}
            />
            <input
              type="number"
              className="form-control"
              placeholder="Enter Amount"
              value={transferAmount}
              onChange={(e) => setTransferAmount(e.target.value)}
            />
          </div>
          <button className="btn btn-warning mt-2" onClick={handleTransferMoney}>
            Transfer Money
          </button>
          <p className='mt-2 text-danger'>{err_msg_transfer_money}</p>
        </div>
      </div>

      {/* Fetch Transactions */}
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Transaction History</h5>
          <button className="btn btn-info mb-2" onClick={handleFetchTransactions}>
            Fetch Transactions
          </button>
          <ul className="list-group">
            {transactions.length > 0 ? (
              transactions.map((transaction, index) => (
                <li key={index} className="list-group-item">
                  <strong>ID:</strong> {transaction.id}, <strong>Type:</strong>{' '}
                  {transaction.transaction_type}, <strong>Amount:</strong>
                  {transaction.amount}, <strong>Date:</strong> {transaction.timestamp}
                </li>
              ))
            ) : (
              <li className="list-group-item">No transactions found.</li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default WalletDashboard;
