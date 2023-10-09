import React from 'react';
import { useNavigate } from 'react-router-dom';
import bg from '../../assets/Loginbg.png';
import Inputbox from '../Inputbox/Inputbox';
import Button from "../Button/Button";


export default function ForgotPasswordCode() {
    const navigate = useNavigate()
    const handleNewPassword=()=>{navigate("/newpassword")}
  return (
    <div
      className="bg-cover bg-center bg-no-repeat min-h-screen flex justify-center items-center"
      style={{ backgroundImage: `url(${bg})` }}
    >
    
    <h1 className='absolute text-white text-2xl font-main-font top-[39%] left-auto'>Enter the 6-digit code sent to your email</h1>
      <form>
        <label className='text-xl font-main-font text-white'>6-digit code</label>
        <Inputbox type="text" id="fname" name="fname" style="flex w-full px-[150px] py-3 my-4 border-2 border-black rounded-md" children={undefined} />
      </form>
      <Button style='absolute top-[60%] right-auto text-sm uppercase py-4 px-14 rounded-full transition font-main-font duration-500 text-white bg-black hover:bg-33B249 hover:text-black'onClick={handleNewPassword}>Continue</Button>
    </div>
  );
}