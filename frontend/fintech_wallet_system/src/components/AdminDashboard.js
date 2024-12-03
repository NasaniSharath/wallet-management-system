import React, { useEffect, useState } from 'react';
import { getAllWallets, getAllTransactions, getAnalytics } from '../services/api';

const AdminDashboard = () => {
  const [wallets, setWallets] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [analyticsData, setAnalyticsData] = useState({});

  useEffect(() => {
    const fetchWallets = async () => {
      try {
        const response = await getAllWallets();
        setWallets(response.data);
      } catch (error) {
        console.error('Error fetching wallets:', error);
      }
    };

    const fetchTransactions = async () => {
      try {
        const response = await getAllTransactions();
        setTransactions(response.data);
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    };

    const fetchAnalytics = async () => {
      try {
        const response = await getAnalytics();
        setAnalyticsData(response.data);
      } catch (error) {
        console.error('Error fetching analytics:', error);
      }
    };

    fetchWallets();
    fetchTransactions();
    fetchAnalytics();
  }, []);

  return (
    <div className="container mt-4">
  <h3 className="text-center mb-4">Admin Dashboard</h3>

  <div className="accordion" id="adminAccordion">
    {/* Wallets Section */}
    <div className="accordion-item">
      <h2 className="accordion-header" id="walletsHeading">
        <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseWallets" aria-expanded="true" aria-controls="collapseWallets">
          All Wallets
        </button>
      </h2>
      <div id="collapseWallets" className="accordion-collapse collapse show" aria-labelledby="walletsHeading" data-bs-parent="#adminAccordion">
        <div className="accordion-body">
          {wallets.length > 0 ? (
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Wallet ID</th>
                  <th>Balance</th>
                </tr>
              </thead>
              <tbody>
                {wallets.map(wallet => (
                  <tr key={wallet.wallet_id}>
                    <td>{wallet.name}</td>
                    <td>{wallet.wallet_id}</td>
                    <td>{wallet.balance}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-danger">No wallets found.</p>
          )}
        </div>
      </div>
    </div>

    {/* Transactions Section */}
    <div className="accordion-item">
      <h2 className="accordion-header" id="transactionsHeading">
        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTransactions" aria-expanded="false" aria-controls="collapseTransactions">
          All Transactions
        </button>
      </h2>
      <div id="collapseTransactions" className="accordion-collapse collapse" aria-labelledby="transactionsHeading" data-bs-parent="#adminAccordion">
        <div className="accordion-body">
          {transactions.length > 0 ? (
            <table className="table table-bordered">
              <thead>
                <tr>
                  <th>Transaction ID</th>
                  <th>Wallet ID</th>
                  <th>Type</th>
                  <th>Amount</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map(tx => (
                  <tr key={tx.id}>
                    <td>{tx.id}</td>
                    <td>{tx.wallet_id}</td>
                    <td>{tx.type}</td>
                    <td>{tx.amount}</td>
                    <td>{new Date(tx.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-danger">No transactions found.</p>
          )}
        </div>
      </div>
    </div>

    {/* Analytics Section */}
    <div className="accordion-item">
      <h2 className="accordion-header" id="analyticsHeading">
        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseAnalytics" aria-expanded="false" aria-controls="collapseAnalytics">
          Analytics Overview
        </button>
      </h2>
      <div id="collapseAnalytics" className="accordion-collapse collapse" aria-labelledby="analyticsHeading" data-bs-parent="#adminAccordion">
        <div className="accordion-body">
          {analyticsData ? (
            <>
              <p><strong>Total Money Added:</strong> {analyticsData.total_money_added}</p>
              <p><strong>Total Transactions:</strong> {analyticsData.total_transactions}</p>
              <h3>Top 5 Wallets</h3>
              <ul className="list-group">
                {analyticsData.top_wallets?.map(wallet => (
                  <li key={wallet.wallet_id} className="list-group-item">
                    {wallet.name} : {wallet.balance}
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p className="text-danger">No analytics data available.</p>
          )}
        </div>
      </div>
    </div>
  </div>
</div>

  );
};

export default AdminDashboard;
