import React, { useState, useEffect } from 'react';
import {addEmployee, fetchAllEmployees,uploadImage,DeleteEmployee,UpdateEmployee}  from '../api/apiservice';
import '../styles/EmployeeForm.css';


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
    //Reload the entire page
    window.location.reload(); 
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

const formatDateTime12Hour = (isoString) => {
   // 1. Remove fractional seconds beyond 3 digits
  // 2. Remove redundant time zone like "+00:00Z" -> just "Z"
  // isoString format like "2025-05-04T07:19:17.892000+00:00Z"
  const cleaned = isoString
    .replace(/\.\d{3,6}/, '')        // remove .xxxxxx
    .replace(/\+00:00Z$/, 'Z');      // replace +00:00Z with Z

  const date = new Date(cleaned);

  // Check if the date is valid
  if (isNaN(date.getTime())) {
    return 'Invalid date';
  }

  // Format to 12-hour time with AM/PM
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  });
};

  return (
    <>
    <div className="employee-form-container">
      <h2>Add Employee</h2>
      <div className='input-field'>
      <input name="employee_id" placeholder="Employee ID" value={form.employee_id} onChange={handleChange} />
      <input name="name" placeholder="Name" value={form.name} onChange={handleChange} />
      <button onClick={handleSubmit}>Add Employee</button>
      </div>
     
    </div>
    
    <hr />
    
    <div className="employee-list-container">
        <h2>All Employees</h2>
        <ul>
          {employees.map((emp) => (
            <li key={emp.employee_id} className="employee-item">
              <div>

{editingId === emp.employee_id ? (
  <>
    <div className="editing-controls">
  <input
    type="text"
    name="name"
    value={editForm.name}
    onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
  />
  <button onClick={() => handleUpdate(emp.employee_id)}>Save</button>
  <button onClick={() => setEditingId(null)}>Cancel</button>
</div>
  </>
) : (
  <>
    <div className="employee-item">
  <div className="employee-cell">
    <div className="cell-heading"><h3>Employee ID</h3></div>
    <div>{emp.employee_id}</div>
  </div>
  <div className="employee-cell">
    <div className="cell-heading"><h3>Name</h3></div>
    <div>{emp.name}</div>
  </div>
  <div className="employee-cell">
    <div className="cell-heading"><h3>Created Time</h3></div>
    <div>{formatDateTime12Hour(emp.created_time)}</div>
  </div>



  <div>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => handleFileChange(emp.employee_id, e)} />
              <button className="btn-upload" onClick={() => handleUpload(emp.employee_id)}>Upload Image</button>
              </div>

  <div className="employee-cell">
  <div className="button-group">
    <button className="btn-edit" onClick={() => startEdit(emp)}>Edit</button>
    <button className="btn-delete" onClick={() => handleDelete(emp.employee_id)}>Delete</button>
  </div>
  </div>

</div>

  </>
)}
              </div>
            </li>
          ))}
        </ul>
      </div>
      </>

   
  )
}

export default EmployeeForm