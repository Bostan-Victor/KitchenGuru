import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import bg from '../../assets/Loginbg.png';
import Inputbox from '../Inputbox/Inputbox';
import Button from '../Button/Button';
import { useState } from 'react';
import { useForm } from 'react-hook-form';

export default function Login() {
  const navigate = useNavigate();
  const handleForgotPassword = () => {
    navigate('/forgotpassword');
  };
  const handleRegister = () => {
    navigate('/register');
  };
  const [data,setdata] = useState()
  const { register, handleSubmit } = useForm();
  const handleButton = (data) => {
    const jsonData = JSON.stringify(data);
    fetch("http://127.0.0.1:8000/api/auth/login", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonData,
    })
    .then(response => response.json())
    .then(data => {
      console.log("Backend Response:", data["access_token"]);
    })
    .catch(error => {
      console.error("Error fetching from backend:", error);
    });
    console.log(data)
  }
  return (
    <div
      className="bg-cover bg-center bg-no-repeat min-h-screen flex justify-center items-center" style={{ backgroundImage: `url(${bg})` }}>
      <h1 className="absolute text-white text-5xl font-main-font top-[15%] left-[30%]">Welcome back!</h1>
      <h1 className="absolute text-white text-xl font-main-font top-[20%] left-[30.5%]">Keep in trend with new recipes!</h1>
      <h1 className="absolute text-white text-5xl font-main-font top-[31%] left-[37%]">Login:</h1>
      <form onSubmit={handleSubmit(handleButton)}>
        <label className="text-xl font-main-font text-white">Nickname or Email</label>
        <Inputbox

          type="text"
          style="flex w-[500px] px-[15px] py-3 my-4 border-2 border-black rounded-md"
          register={register("username_email")}
        />
        <label className="text-xl font-main-font text-white">Password</label>
        <Inputbox
          type="password"
          style="w-full px-5 py-3 my-2 border-2 border-black rounded-md"
          register={register("password")}
        />
        <Button
          style="fixed top-[65%] right-[38%] text-sm uppercase py-4 px-14 rounded-full transition font-main-font duration-500 text-white bg-black hover:bg-33B249 hover:text-black"
        >
          <input type="submit" value="Login"/>
        </Button>
      </form>
      <Button
        style=" fixed top-[61%] right-[55%] font-main-font text-white"
        onClick={handleForgotPassword}
      >
        Forgot password?
      </Button>
      <Button
        style=" fixed top-[61%] right-[38%] font-main-font text-white"
        onClick={handleRegister}
      >
        Don’t have an account?
      </Button>
    </div>
  );
}