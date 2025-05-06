import React from 'react';
import EmployeeForm from './components/EmployeeForm.js';
import ImageUpload from './components/ImageUpload';
import QueryImages from './components/QueryImages';

const App = () => {
  return (
    <div>
      <h1>DRMS - Admin Dashboard</h1>
      <EmployeeForm />
      <ImageUpload />
      <QueryImages />
    </div>
  );
};

export default App;
