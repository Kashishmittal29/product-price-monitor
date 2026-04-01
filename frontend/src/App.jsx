import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [products, setProducts] = useState([]);
  const [stats, setStats] = useState(null);

  const fetchData = async () => {
    try {
      // Fetch overview stats
      const statsRes = await axios.get('http://localhost:8000/api/v1/analytics/overview');
      setStats(statsRes.data);

      // Fetch products list
      const productsRes = await axios.get('http://localhost:8000/api/v1/products?limit=50');
      setProducts(productsRes.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const triggerRefresh = async () => {
    try {
      await axios.post('http://localhost:8000/api/v1/jobs/refresh', null, {
        headers: { 'X-API-Key': 'secret-token-123' }
      });
      alert("Refresh Job Triggered! (Check backend logs and refresh this page shortly)");
      fetchData();
    } catch (err) {
      console.error(err);
      alert("Failed to trigger refresh. Is the backend running?");
    }
  };

  return (
    <div className="min-h-screen p-8 text-gray-800 font-sans">
      <header className="mb-8 flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-800">Product Price Monitor</h1>
          <p className="text-slate-500 text-sm mt-1">Real-time tracking of luxury goods and electronics across platforms.</p>
        </div>
        <button 
          onClick={triggerRefresh}
          className="bg-indigo-600 font-semibold text-white px-5 py-2.5 rounded-lg shadow-md hover:bg-indigo-700 transition"
        >
          Refresh Data Files
        </button>
      </header>

      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h3 className="text-slate-500 text-xs font-bold tracking-wider uppercase">Total Tracked</h3>
            <p className="text-4xl font-extrabold text-slate-800 mt-2">{stats.total_products}</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col justify-center">
            <h3 className="text-slate-500 text-xs font-bold tracking-wider uppercase mb-3">Data Sources</h3>
            <div className="flex gap-2 flex-wrap">
              {stats.sources.length === 0 && <span className="text-sm text-slate-400">No sources found</span>}
              {stats.sources.map(s => (
                <span key={s} className="bg-indigo-50 border border-indigo-100 text-indigo-700 text-xs px-3 py-1.5 rounded-full font-medium shadow-sm capitalize">{s}</span>
              ))}
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col justify-center">
            <h3 className="text-slate-500 text-xs font-bold tracking-wider uppercase mb-3">Avg Price by Category</h3>
            <div className="space-y-2">
              {stats.avg_prices && stats.avg_prices.length === 0 && <span className="text-sm text-slate-400">No data</span>}
              {stats.avg_prices && stats.avg_prices.map(c => (
                <div key={c.category} className="flex justify-between items-center text-sm">
                  <span className="text-slate-600 truncate mr-2">{c.category}</span>
                  <span className="font-semibold">${c.avg_price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-8">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-bold mb-6 text-slate-800">Latest Processed Items</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {products.map(p => (
              <div key={p.id} className="bg-slate-50 p-5 rounded-lg border border-slate-200 transition hover:shadow-md hover:border-slate-300">
                <div className="flex justify-between items-start mb-3">
                  <span className="text-[10px] bg-slate-200 text-slate-600 font-bold px-2 py-0.5 rounded tracking-wide uppercase">{p.source}</span>
                  <span className="text-xs text-slate-400 flex items-center gap-1">
                     <svg className="w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                    {new Date(p.last_updated).toLocaleDateString()}
                  </span>
                </div>
                <h4 className="font-bold text-base leading-tight mb-1 text-slate-900">{p.brand}</h4>
                <p className="text-sm text-slate-600 mb-4 line-clamp-1">{p.name}</p>
                <div className="flex justify-between items-end mt-auto pt-3 border-t border-slate-200">
                  <span className="text-xs text-slate-500 uppercase">{p.category}</span>
                  <span className="text-xl font-extrabold text-emerald-600">${p.current_price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                </div>
              </div>
            ))}
          </div>
          {products.length === 0 && (
            <div className="py-12 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 mb-4">
                 <svg className="w-8 h-8 text-slate-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m8.25 3v6.75m0 0-3-3m3 3 3-3M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
                </svg>
              </div>
              <p className="text-slate-500 font-medium">No products track records yet.</p>
              <p className="text-slate-400 text-sm mt-1">Place your initial datasets in the `data/` folder and click "Refresh Data Files".</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
