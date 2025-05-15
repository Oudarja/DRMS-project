import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import EmployeeForm from './components/EmployeeForm.js';
import QueryImages from './components/QueryImages';
import './App.css';
import ScrollButtons from './components/ScrollButton.js';

const NavLinks = () => {
  // useLocation is a React Hook provided by React Router that 
  // allows you to access the current location object, which 
  // represents the current URL in your application.
  /*
  It gives you details about the current route, such as:
  ->The pathname (URL path),
  ->Any search query parameters,
  ->The hash fragment,
  ->And state if passed via navigation
  */
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
