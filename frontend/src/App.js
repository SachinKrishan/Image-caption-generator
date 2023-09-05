import React, { useState } from 'react';

const ImageUploadForm = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [responseText, setResponseText] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      alert('Please select an image file');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/mlmodel/generate_caption/', {
        method: 'POST',
        body: formData,
      });


      if (response.ok) {
        const data = await response.json();
        // Display the 'caption' property of the response object
        setResponseText(data.caption);
      } else {
        const data = await response.json();
        setResponseText(data);
      }
    } catch (error) {
      console.error('Error:', error);
      setResponseText('Error uploading image');
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit">Upload Image</button>
      </form>
      {responseText && <div>Response: {responseText}</div>}
    </div>
  );
};

export default ImageUploadForm;