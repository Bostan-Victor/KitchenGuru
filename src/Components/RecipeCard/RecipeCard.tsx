import React from 'react';

interface ACarD {
  title?: string;
  image?: string;
  style?: string;
  onClick?:()=>void;
  id?:number;
}

export default function RecipeCard({ title, image, style, onClick, id }: ACarD) {
  return (
    <div className=" flex-col items-center inline-block sm:w-64 mx-20">
      <div className='text-center mt-12 break-words' onClick={onClick}>
        <img src={image ? "http://dummyimage.com/240" : "http://dummyimage.com/240"} alt="recipe" className={`${style}`} />
        <h1>{title}</h1>
      </div>
    </div>
  );
}
