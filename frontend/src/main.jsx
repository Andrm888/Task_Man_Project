import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

// CssBaseline - это "сброс" стилей CSS для всего браузера
import CssBaseline from '@mui/material/CssBaseline';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* "Оборачиваем" наше приложение в CssBaseline */}
    <CssBaseline />
    <App />
  </React.StrictMode>
);
