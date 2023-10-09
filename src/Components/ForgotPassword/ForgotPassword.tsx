import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import bg from '../../assets/Loginbg.png';
import Inputbox from '../Inputbox/Inputbox';
import Button from "../Button/Button";
import axios from 'axios';
import { useForm } from 'react-hook-form';


export default function ForgotPassword() {
  const navigate = useNavigate()
  const handleRegister=()=>{navigate("/register")}
  const handleForgotPasswordCode=()=>{navigate("/newpassword")}

  const { register, handleSubmit } = useForm();
  const [data, setData] = useState("");
  const handleButton = (e) => {
    e.preventDefault();
    console.log("named")
    const jsonData = JSON.stringify(data);
    axios.post("http://127.0.0.1:8000/api/auth/password-recovery-request", jsonData)
      .then((response) => console.log(response.data));
  };
  return (
    <div
      className="bg-cover bg-center bg-no-repeat min-h-screen flex justify-center items-center"
      style={{ backgroundImage: `url(${bg})` }}
    >
    <h1 className='absolute text-white text-2xl font-main-font top-[36%] left-auto'>Enter the email address of your account and we’ll </h1>
    <form onSubmit={handleButton}>
        <label className='text-xl font-main-font text-white'>Email</label>
        <Inputbox type="text" register={register("email")} id="fname" name="fname" style="flex w-full px-[150px] py-3 my-4 border-2 border-black rounded-md" children={undefined} />
        <button type='submit'>Submit</button>
      </form>
      <Button style='absolute top-[56%] right-[53%] font-main-font text-white' onClick={handleRegister}>Don’t have an account?</Button>
      {/* <Button style='absolute top-[60%] right-auto text-sm uppercase py-4 px-14 rounded-full transition font-main-font duration-500 text-white bg-black hover:bg-33B249 hover:text-black' type="submit">Continue</Button> */}
    </div>
  );
}