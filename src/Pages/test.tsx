import React from "react";
import Navbar from "../Components/Navbar";
import fork from '../helpers/bg.png'; // Update the import paths to be relative to your project structure
import plate from '../helpers/homapageplate.png'; // Update the import paths

function TestPage() {
  return (
    <>
      <Navbar /> {/* Include your Navbar component */}
      <div>
        <h1>hi</h1>
        <img src={fork} alt="Fork" />
        <img src={plate} alt="Plate" />
      </div>
    </>
  );
}

export default TestPage;
