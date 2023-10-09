import React from 'react';
import data from '../../assets/recipes.json';
import Navbar from "../../Components/Navbar";
import RecipeCart from '../RecipeCard/RecipeCard';
import Button from '../Button/Button';
import { Link, useNavigate, useParams } from 'react-router-dom';


export default function Recipe() {
  const handleClick = (title) => {
    let id = title
    // console.log(id);
  };
  const navigate = useNavigate();
  const {id}= useParams();

  console.log(id)

  const handleDiplay = () => {
    navigate('/recipedisplay/2');
  };

  return (
    <div className='flex items-center justify-center mt-12 sm:mt-20'>
      <div className='flex flex-wrap justify-center'>
        {data.slice(0, 6).map((el: any,i) => (
          <div className='w-full sm:w-1/3 p-2 space-y-8' key={el.title}>
            <Link to={`/reciepdsiplay/${el.id}`}>
            <RecipeCart
              image={el.image} 
              title={el.title} 
              onClick={() => handleClick(el.title)}
            />
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}