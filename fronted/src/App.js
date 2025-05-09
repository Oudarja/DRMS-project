import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import EmployeeForm from './components/EmployeeForm.js';
import QueryImages from './components/QueryImages';
import './App.css';

const NavLinks = () => {
  const location = useLocation();

  return (
    <nav>
      <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Home</Link>
      <Link to="/query" className={location.pathname === '/query' ? 'active' : ''}>Query</Link>
    </nav>
  );
};

const App = () => {
  return (
    <Router>
      <div className="app-container">
        <h1>Digital Resource Management System</h1>
        <NavLinks />
        <Routes>
          <Route path="/" element={<EmployeeForm />} />
          <Route path="/query" element={<QueryImages />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
