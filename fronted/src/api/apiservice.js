/*
The purpose of apiService.js is to act as a centralized utility file for 
managing all your frontend API calls (usually to your backend — like FastAPI, Node.js, etc.).
apiService.js separates concerns, promotes code reuse, and simplifies maintenance in projects
that communicate with a backend like your FastAPI server.
*/

// Axios is a client-side HTTP library used in your React frontend 
// to make requests to my FastAPI backend.
import axios from 'axios';

import qs from 'qs';

// Fast api is running on port 8000 on local device
const API_BASE_URL = 'http://127.0.0.1:8000'; 


// All api call associated with employee
export const addEmployee = async (employeeData) => {
    return axios.post(`${API_BASE_URL}/employees/add-employee`, employeeData);
  };

  export const fetchAllEmployees = async () => {
    const response = await axios.get(`${API_BASE_URL}/employees/get-all-employee`);
    return response.data;
  };
// update employee
export const UpdateEmployee=async(employee_id,updatedData)=>
{
    const response = await axios.put(
        `${API_BASE_URL}/employees/update-employee/${employee_id}`, updatedData);
    return response.data;
}

// delete employee

export const DeleteEmployee=async(employee_id)=>
{
    const response = await axios.delete(`${API_BASE_URL}/employees/delete-employee/${employee_id}`);
    return response.data;
}




// All API call associated with images
export const uploadImage = async (formData) => {
  return axios.post(`${API_BASE_URL}/images/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};
// qs is for serealizing , Axios doesn't serialize array params into repeated query strings by default
// But Fast Api expects serialized repeated query string like /images/query?tags=cat&tags=plane
// configure Axios to serialize arrays properly.

export const queryImages = async (employeeId, tags) => 
{
  
  const params = {};

  if (employeeId)
     params.employee_id = employeeId;
  
  if (tags) {
    // Convert comma-separated string to array
    // .trim() function in JavaScript is used to remove 
    // leading and trailing whitespace from a string.
    const tagList = tags.split(',').map(t => t.trim());
    // taglist contains all tag that were passed from fronted UI by user 
    // and they are trimmed and commas are removed from them
    tagList.forEach(tag => 
    {
      if (!params.tags) 
        params.tags = [];

      params.tags.push(tag);
    });
  }
  //  console.log(params)

  const res = await axios.get(`${API_BASE_URL}/images/query`, { params ,
    paramsSerializer: params => qs.stringify(params, { arrayFormat: 'repeat' }),
});
  console.log(res)
  return res.data.message;
};


export const deleteImage=async (employee_id)=>
{
    const response = await axios.delete(`${API_BASE_URL}/images/image/delete/${employee_id}`);

    return response.data;
}

// Axios is used inside apiService.js file (or sometimes directly inside components).
// React calls Axios → Axios sends request → FastAPI receives → responds → Axios returns the
// result → React renders it.
