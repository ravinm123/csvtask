// src/components/ProcessedData.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles.css';

const ProcessedData = ({ fileId }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/processed/${fileId}/`);
        setData(response.data);
      } catch (error) {
        console.error('Error fetching processed data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [fileId]);

  if (loading) return <p>Loading...</p>;
  if (!data) return <p>No data available.</p>;

  return (
    <div>
      <h2>Processed Data</h2>
      <ul>
        <li>Total Revenue: {data.total_revenue}</li>
        <li>Average Discount: {data.avg_discount}</li>
        <li>Best Selling Product: {data.best_selling_product}</li>
        <li>Most Profitable Product: {data.most_profitable_product}</li>
        <li>Max Discount Product: {data.max_discount_product}</li>
      </ul>
    </div>
  );
};

export default ProcessedData;