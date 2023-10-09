import { Link, useNavigate, useParams } from 'react-router-dom';
import avatar from "../../assets/image 25.png"
import Inputbox from '../Inputbox/Inputbox';
import { useForm } from 'react-hook-form';
import { useState } from 'react';

export default function Settings() {
    const { register, handleSubmit } = useForm();
    const [data, setData] = useState("");
  return (
    <div>
        <img className="w-[150px] ml-[5%] mr-[7%]" src={avatar} alt="Avatar" />
        <span className="mt-[6%] font-main-font text-2xl">Nickname</span>
    </div>
  );
}