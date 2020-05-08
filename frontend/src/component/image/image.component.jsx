import React from 'react'

export function Image(props) {
    const uploadedImage = React.useRef(null);
    const imageUploader = React.useRef(null);

    const handleImageUpload = e => {
      const [file] = e.target.files;
      if (file) {
        const reader = new FileReader();
        const { current } = uploadedImage;
        reader.onload = e => {
          current.src = e.target.result;
          props.onUpload(current.src);
        };
        reader.readAsDataURL(file);
      }
    };

    return (
      <div>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          ref={imageUploader}
          style={{
            display: "none"
          }}
        />
        <div
          style={{
            height: "500px",
            width: "500px",
            border: "1px dashed black",
            margin:'20px'
          }}
          onClick={ () => imageUploader.current.click()}
        >
          <img
            ref={uploadedImage}
            style={{
              width: "100%",
              height: "100%"
            }}
          />
        </div>
        
      </div>
    );
  }
  