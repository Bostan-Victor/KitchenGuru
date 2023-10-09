import React from 'react';
import { useNavigate } from 'react-router-dom';
import bg from '../../assets/Loginbg.png';
import Inputbox from '../Inputbox/Inputbox';
import Button from "../Button/Button";


export default function NewPassword() {
  return (
    <div
      className="bg-cover bg-center bg-no-repeat min-h-screen flex justify-center items-center"
      style={{ backgroundImage: `url(${bg})` }}
    >
      <form>
        <label className='text-xl font-main-font text-white'>Enter new password:</label>
        <Inputbox type="text" id="fname" name="fname" style="flex w-full px-[150px] py-3 my-4 border-2 border-black rounded-md" children={undefined} />
        <label className='text-xl font-main-font text-white'>Repeat new password:</label>
        <Inputbox type="text" id="fname" name="fname" style="flex w-full px-[150px] py-3 my-4 border-2 border-black rounded-md" children={undefined} />
      </form>
      <Button style='absolute top-[65%] right-auto text-sm uppercase py-4 px-14 rounded-full transition font-main-font duration-500 text-white bg-black hover:bg-33B249 hover:text-black'>Confirm</Button>
    </div>
  );
}