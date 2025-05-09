import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import EmployeeForm from './components/EmployeeForm.js';
import QueryImages from './components/QueryImages';
import './App.css';
import ScrollButtons from './components/ScrollButton.js';

const NavLinks = () => {
  const location = useLocation();

  return (
    <nav>
      <div className='nav-link'>
      <h3><Link to="/" className={location.pathname === '/' ? 'active' : ''}>Home</Link></h3>
      <h3><Link to="/query" className={location.pathname === '/query' ? 'active' : ''}>Query</Link></h3>
      </div>
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
        <ScrollButtons/>
      </div>
    </Router>
  );
};

export default App;
