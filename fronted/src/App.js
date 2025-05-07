import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import EmployeeForm from './components/EmployeeForm.js';
import QueryImages from './components/QueryImages';

const App = () => {
  return (
    <Router>
      <div>
        <h1>DRMS Web App</h1>
        <nav>
          <Link to="/">Home</Link> | <Link to="/query">Query</Link>
        </nav>

        <Routes>
          <Route path="/" element={<EmployeeForm />} />
          <Route path="/query" element={<QueryImages />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
