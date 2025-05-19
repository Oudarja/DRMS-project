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
      // Clear previous results
      setResults([]); 
      // console.log(tags)
      const data = await queryImages(empId, tags);
      // console.log(data);
      setResults(data);
    } catch (err) {
      console.error("Query failed", err);
      alert("Error querying images.");
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
    <div className="query-container">


{/* Conditional rendering */}

{results.length == 0 ? (

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
        
        {
         results.map((res, idx) => {
         const fullUrl = res.url
         const tags = res.tags?.join(', ') || 'No tags';
         const uploadTime = res.upload_time || 'Unknown';
         const size = res.size || 'Unknown';
  // console.log(fullUrl)
  return (
    // <li key={idx}>
    //   <img src={fullUrl} alt={`Result ${idx}`} width="200" />
    //   <div><strong>Tags:</strong> {tags}</div>
    //   <div><strong>Uploaded:</strong> {uploadTime}</div>
    //   <div><strong>Size:</strong> {size} bytes</div>
    // </li>
    <li key={idx}>
    <img src={fullUrl} alt={`Result ${idx}`} width="200" />
    <div className="meta">
      <p><strong>Tags:</strong> {tags}</p>
      <p><strong>Uploaded Time:</strong> { formatDateTime12Hour(uploadTime)}</p>
      <p><strong>Size:</strong> {size} Bytes</p>
    </div>
  </li>
  );
})
}
      </ul>
      </>
)
}
    </div>

  );
}

export default QueryImages