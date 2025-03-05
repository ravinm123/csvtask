// src/App.js
import React from 'react';
import FileUpload from './components/FileUpload';
import ProcessedData from './components/ProcessedData';
import ProductSearch from './components/ProductSearch';

function App() {
  const [fileId, setFileId] = React.useState(null);

  return (
    <div className="App">
      <h1>CSV Processor</h1>
      <FileUpload />
      {fileId && <ProcessedData fileId={fileId} />}
      <ProductSearch />
    </div>
  );
}

export default App;