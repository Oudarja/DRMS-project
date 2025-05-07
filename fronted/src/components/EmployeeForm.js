import React, { useState, useEffect } from 'react';
import {addEmployee, fetchAllEmployees,uploadImage,DeleteEmployee,UpdateEmployee}  from '../api/apiservice';

const EmployeeForm = () => {


    const [form,setForm]=useState({
      employee_id:'',
      name:'',
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
    setForm({ employee_id: '', name: '' });
    const data=await fetchAllEmployees();
    setEmployees(data);
    }
    catch(error){
        console.log("Add employee fail",error)
        alert("Error adding employee");
    }
};

// This state is a dictionary/object where each key is an employee_id and value is the selected image file.
const [selectedFiles, setSelectedFiles] = useState({});
/*
Triggered when a user selects a file in the file input.

It grabs the selected file from the event and stores it in
selectedFiles using the employee's ID as key.
*/
const handleFileChange = (empId, e) => {
  // In the context of selecting an image using an <input type="file">, the 
  // "first file" means the first image file selected by the user from their file dialog.
  const file = e.target.files[0];
  setSelectedFiles((prev) => ({ ...prev, [empId]: file }));
};
/*
->It first checks if a file was selected for the given empId.

->Creates a new FormData() object (used for file uploads).

->Appends the selected file to it under the key "file".

->Sends this formData to your backend via the uploadImage(empId, formData) 
function (which must be defined in apiservice.js).

->If successful, shows success message. If not, shows an error.


*/

const handleUpload = async (empId) => {
  if (!selectedFiles[empId]) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFiles[empId]);
  // Send employee_id in the form
  formData.append("employee_id", empId);

  try {
    // pass only form data now which has both employee id and image file
    await uploadImage(formData);
    alert("Image uploaded successfully!");
  } catch (error) {
    console.error("Image upload failed:", error);
    alert("Upload failed.");
  }
};

// edit

const [editingId, setEditingId] = useState(null);
// updation done on only name
const [editForm, setEditForm] = useState({ name: '' });

const startEdit = (emp) => {
  setEditingId(emp.employee_id);
  setEditForm({ name: emp.name });
};

const handleUpdate = async (empId) => {
  try {
    await UpdateEmployee(empId, editForm);
    const data = await fetchAllEmployees();
    setEmployees(data);
    setEditingId(null);
  } catch (err) {
    alert("Update failed");
    console.error(err);
  }
};


// delete

const handleDelete = async (empId) => {
  if (!window.confirm("Are you sure you want to delete this employee?"))
        return;

  try {
    await DeleteEmployee(empId);
    const data = await fetchAllEmployees();
    setEmployees(data);
  } catch (err) {
    alert("Delete failed");
    console.error(err);
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
    <input name="employee_id" placeholder="Employee ID" value={form.employee_id} onChange={handleChange} />
    <input name="name" placeholder="Name" value={form.name} onChange={handleChange} />
    <button onClick={handleSubmit}>Add Employee</button>
    </div>

    <hr />
    <div>
    <h3>All Employees</h3>
    <ul>

    {employees.map((emp) => (
  <li key={emp.employee_id}>
    <div>
      {editingId === emp.employee_id ? (
        <>
          <input
            type="text"
            name="name"
            value={editForm.name}
            onChange={(e) =>
              setEditForm({ ...editForm, name: e.target.value })
            }
          />
          <button onClick={() => handleUpdate(emp.employee_id)}>Save</button>
          <button onClick={() => setEditingId(null)}>Cancel</button>
        </>
      ) : (
        <>
          <strong>{emp.name}</strong> — 
          <strong>ID: {emp.employee_id}</strong> — 
          <strong>Created Time: {emp.created_time}</strong>
          <button onClick={() => startEdit(emp)}>Edit</button>
          <button onClick={() => handleDelete(emp.employee_id)}>Delete</button>
        </>
      )}
    </div>

    {/* Image upload section (as before) */}
    <div>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => handleFileChange(emp.employee_id, e)}
      />
      <button onClick={() => handleUpload(emp.employee_id)}>Upload Image</button>
    </div>

  </li>
))}

    </ul>
    </div>
  </div>
  )
}

export default EmployeeForm