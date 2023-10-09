import React from 'react';
import data from '../../assets/recipes.json';
import Navbar from "../../Components/Navbar";
import RecipeCart from '../RecipeCard/RecipeCard';
import Button from '../Button/Button';
import { Link, useNavigate, useParams } from 'react-router-dom';
import Inputbox from '../Inputbox/Inputbox';

export default function Top() {
  const handleClick = (title) => {
    let id = title;
    // console.log(id);
  };

  const navigate = useNavigate();
  const {id} = useParams();

  console.log(id)

  const handleDiplay = () => {
    navigate('/recipedisplay/2');
  };

  return (
    <>
    <Navbar/>
    <div className='flex'>
    <div className='flex-1 items-start justify-center mt-12 sm:mt-20 '>
      <div className='flex-2 p-4 mt-[5%]'>
        <div className='flex flex-wrap justify-center'>
          {data.slice(0, 6).map((el: any, i) => (
            <div className='w-full sm:w-1/2 lg:w-1/3 p-2 space-y-8' key={el.title}>
              <Link to={`/reciepdsiplay/${el.id}`}>
              <RecipeCart
                image={el.image} 
                title={el.title} 
                onClick={() => handleClick(el.title)}
                style='relative'
              />
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
      <div className='flex justify-center items-center h-screen text-3xl font-main-font'>
        <span className='absolute mr-[17%] mt-[-30%] whitespace-nowrap'>Sort by:</span>
      </div>
    <div className="absolute p-4 font-main-font text-xl bottom-[18%] left-[86.5%]">
  <div className="flex flex-col items-center justify-center h-screen">
    <div className="bg-green-400 p-4 rounded-lg shadow-lg">
      <div className="flex flex-col items-start space-y-4">
        <div className="flex items-center">
          <input type="radio" name="options" id="option1" className="form-radio text-green-600 h-6 w-6" />
          <label className="text-white ml-4 text-lg">Rating</label>
        </div>
        <div className="flex items-center">
          <input type="radio" name="options" id="option2" className="form-radio text-green-600 h-6 w-6" />
          <label className="text-white ml-4 text-lg">Comments</label>
        </div>
        <div className="flex items-center">
          <input type="radio" name="options" id="option3" className="form-radio text-green-600 h-6 w-6" />
          <label className="text-white ml-4 text-lg">Favorites</label>
        </div>
      </div>
    </div>
  </div>
  <div className='absolute left-[12%] top-[63%] font-main-font'>
    <span>Duration</span>
    <div className='absolute flex flex-row items-center'>
      <Inputbox style='w-12 border border-green-500' placeholder = "0" />
      <span className='mx-2'>-</span>
      <Inputbox style='w-12 border border-green-500' placeholder = "300" />
      <span className='mx-2 text-base'>minutes</span>
    </div>
  </div>
  <div className='absolute text-xl font-main-font top-[73%] left-[25%]'>
    <span>Select Food Categories:</span>
  </div>
  <div className="absolute flex flex-col items-center justify-center h-screen top-[48%] left-[13.5%]">
  <div className="bg-green-400 p-4 rounded-lg shadow-lg">
    <div className="flex flex-col items-start space-y-4">
      <div className="flex items-center">
        <input type="checkbox" name="options" id="option1" className="form-checkbox text-green-600 h-6 w-6" />
        <label className="text-white ml-4 text-lg">Drinks</label>
      </div>
      <div className="flex items-center">
        <input type="checkbox" name="options" id="option2" className="form-checkbox text-green-600 h-6 w-6" />
        <label className="text-white ml-4 text-lg">Desserts</label>
      </div>
      <div className="flex items-center">
        <input type="checkbox" name="options" id="option3" className="form-checkbox text-green-600 h-6 w-6" />
        <label className="text-white ml-4 text-lg">Soups</label>
      </div>
      <div className="flex items-center">
        <input type="checkbox" name="options" id="option1" className="form-checkbox text-green-600 h-6 w-6" />
        <label className="text-white ml-4 text-lg">Salads</label>
      </div>
      <div className="flex items-center">
        <input type="checkbox" name="options" id="option1" className="form-checkbox text-green-600 h-6 w-6" />
        <label className="text-white ml-4 text-lg">Meat</label>
      </div>
      <div className="flex items-center">
        <input type="checkbox" name="options" id="option1" className="form-checkbox text-green-600 h-6 w-6" />
        <label className="text-white ml-4 text-lg">Seafood</label>
      </div>
      <div className="flex items-center">
        <input type="checkbox" name="options" id="option1" className="form-checkbox text-green-600 h-6 w-6" />
        <label className="text-white ml-4 text-lg">Others</label>
      </div>
    </div>
  </div>
</div>
</div>
    </div>
    </>
  );
}
