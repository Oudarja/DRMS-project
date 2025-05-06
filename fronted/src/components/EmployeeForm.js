import React, { useState, useEffect } from 'react';
import {addEmployee, fetchAllEmployees}  from '../api/apiservice';

const EmployeeForm = () => {


    const [form,setForm]=useState({
        id:'',
        name:'',
        created_time:'',
    })

    // Here list as i will handle with list of employee
    // from database to show in ui
    const [employees,setEmployees]=useState([])


    useEffect(()=>{
        const loadEmployees=async ()=>
        {
            try {
            const data=await fetchAllEmployees();
            setEmployees(data);
            }
            catch(error){
                console.error("Failed to fetch employees:", error);
            }
        };
        loadEmployees();
    },[]
);

const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

const handleSubmit=async()=>{
    try{
    await addEmployee(form);
    setForm({id:'',name:''});
    const data=await fetchAllEmployees();
    setEmployees(data);
    }
    catch(error){
        console.log("Add employee fail",error)
        alert("Error adding employee");
    }
};

// const formatDate = (isoString) => {
//     const date = new Date(isoString);
//     return date.toISOString().replace('T', ' ').split('.')[0];  // "2025-05-04 07:19:17"
//   };

  return (
    <div>
    <div>
    <h2>Add Employee</h2>
    <input name="id" placeholder="Employee ID" value={form.id} onChange={handleChange} />
    <input name="name" placeholder="Name" value={form.name} onChange={handleChange} />
    <button onClick={handleSubmit}>Add Employee</button>
    </div>

    <hr />
    <div>
    <h3>All Employees</h3>
    <ul>
      {employees.map(emp => (
        <li key={emp.employee_id}>
        <strong>{emp.name}</strong> — 
        <strong>ID: {emp.employee_id}</strong> — 
        <strong>Created Time: {emp.created_time}</strong>
        {/* .....here option for image upload which will handle api call */}
      </li>
      ))}
    </ul>
    </div>
  </div>
  )
}

export default EmployeeForm