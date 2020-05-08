import React, {useState} from 'react';
import axios from 'axios'
import logo from './logo.svg';
import './App.css';
import {Header} from './component/header/header.component'
import {Image} from './component/image/image.component'

function App() {
  let [image1, setImage1] = useState('')
  let [image2, setImage2] = useState('')
  let [message, setMessage] = useState('')
  function handleImage1Upload(image){
    setImage1(image)
  }
  function handleImage2Upload(image){
    setImage2(image)
  }
  function handleSubmit(e){
    if (image1 === null || image2 === null){
      setMessage("Please Upload the images")
     }
      const images = {
        image1:image1,
        image2:image2
      }
      console.log(images)
      axios.post(`http://localhost:5000/compare`,  images )
      .then(res => {
        console.log(res.data.result);
      })

    }


  return (
    <div>
      <Header />
      <div className = 'image_container'>
                <Image key = {0} onUpload={handleImage1Upload}/>
                <Image key = {1} onUpload={handleImage2Upload}/>
        </div>
      <button onClick= {handleSubmit} style={{display:'block',height:'30px',width:'150px',border:'none',margin:'auto',borderRadius:'10px',backgroundColor:'blue',color:'white'}}> Compare Images </button>
      <h1>{message}</h1>
    </div>
  );
}

export default App;
