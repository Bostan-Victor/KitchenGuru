import { Link, useNavigate, useParams } from 'react-router-dom';
import data from '../../assets/recipes.json';
import RecipeCart from '../RecipeCard/RecipeCard';
import avatar from "../../assets/image 25.png"


export default function UserInfo() {
    const handleClick = (title) => {
        let id = title
      };
      const navigate = useNavigate();
      const {id}= useParams();
  return (
<div>
  <div className="absolute h-[7%] w-[12px] rounded-full bg-33B249 ml-[-2.1%] mt-[13.5%]"></div>
    <div className="flex flex-col w-full p-4 mt-[3%]">
        <div className="flex ml-[1%]">
        <img className="w-[200px] ml-[5%] mr-[7%]" src={avatar} alt="Avatar" />
        <span className="mt-[6%] font-main-font text-3xl">Nickname</span>
    </div>
    <div className='flex flex-wrap justify-center sm:mt-20 text-base'>
      {data.slice(0, 6).map((el: any, i) => (
        <div className='w-full sm:w-1/3 space-y-4' key={el.title}>
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
</div>
  );
}