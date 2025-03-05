// src/components/ProductSearch.js
import React, { useState } from 'react';
import axios from 'axios';
import '../styles.css';

const ProductSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
        const response = await axios.get(`http://localhost:8000/api/search/?q=${query}`);
      setResults(response.data);
    } catch (error) {
      console.error('Error searching products:', error);
    }
  };

  return (
    <div>
      <h2>Search Products</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter product name"
      />
      <button onClick={handleSearch}>Search</button>

      <ul>
        {results.map((product, index) => (
          <li key={index}>
            {product['Product Name']} - Sales: {product.Sales}, Quantity: {product.Quantity}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProductSearch;