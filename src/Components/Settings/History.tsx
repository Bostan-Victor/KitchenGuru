import { Link, useNavigate, useParams } from 'react-router-dom';
import data from '../../assets/recipes.json';
import RecipeCart from '../RecipeCard/RecipeCard';
import avatar from "../../assets/image 25.png"
import Button from "../Button/Button"

export default function History() {
    const handleClick = (title) => {
        let id = title
      };
      const navigate = useNavigate();
      const {id}= useParams();
  return (
    <div className="mt-[5%]">
  <div className="flex font-main-font text-xl mt-[-2%] ml-[83%]">
    <span className="mt-[7%]"><Button>Nickname</Button></span>
    <Button><img className="ml-[20%]" src={avatar} alt="" /></Button>
  </div>
<div>
  <div className="absolute h-[7%] w-[12px] rounded-full bg-33B249 ml-[-1.85%] mt-[11%]"></div>
    <div className='flex flex-wrap sm:mt-20 text-base'>
      {data.slice(0, 6).map((el: any, i) => (
        <div className='w-full sm:w-1/3 p-2 space-y-4' key={el.title}>
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