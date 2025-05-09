import React,{ useState } from 'react'
import { queryImages } from '../api/apiservice';
import '../styles/QueryImage.css';

const QueryImages = () => {
  const [empId, setEmpId] = useState('');
  // I am taking input from a string box (not a multi-select), so 
  // store it as a string, and let apiService.js convert it to an 
  // array in which format FastAPI expects to receive.
  const [tags, setTags] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {

      // console.log(tags)
      const data = await queryImages(empId, tags);
      // console.log(data);
      setResults(data);
    } catch (err) {
      console.error("Query failed", err);
      alert("Error querying images.");
    }
  };

  return (
    <div className="query-container">


{/* Conditional rendering */}

{results.length ==0 ? (

<>
      <h2>Search Images</h2>

      <div>
        <label><strong>Search by Employee ID:</strong></label><br />
        <input
          value={empId}
          onChange={(e) => setEmpId(e.target.value)}
          placeholder="Enter Employee ID"
        />
      </div>

      <div>
        <label><strong>Search by Tags (comma-separated):</strong></label><br />
        <input
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          placeholder="e.g., person,car,dog"
        />
      </div>

      <button onClick={handleSearch}>Search</button>
      </>

):(
<>
      <hr />
      
      <h2>Search Images</h2>

      <div>
        <label><strong>Search by Employee ID:</strong></label><br />
        <input
          value={empId}
          onChange={(e) => setEmpId(e.target.value)}
          placeholder="Enter Employee ID"
        />
      </div>

      <div>
        <label><strong>Search by Tags (comma-separated):</strong></label><br />
        <input
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          placeholder="e.g., person,car,dog"
        />
      </div>

      <button onClick={handleSearch}>Search</button>
      <h3>Results</h3>
      <ul>

        {/*
           idx is index.It's the second parameter of the .map() 
           function, which represents the position of the current
           element in the array. 
        */}
        
        {results.map((path, idx) => {
  const fullUrl = path
  // console.log(fullUrl)
  return (
    <li key={idx}>
      <img src={fullUrl} alt={`Result ${idx}`} width="200" />
    </li>
  );
})}
      </ul>
      </>
)
}
    </div>

  );
}

export default QueryImages