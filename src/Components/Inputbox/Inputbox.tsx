import React, { ReactNode, ForwardedRef } from 'react';

interface IInputboxProps {
  style?: string;
  type?: string;
  id?: string;
  name?: string;
  children?: ReactNode;
  register?: any;
  placeholder?: string;
}

const Inputbox = React.forwardRef<HTMLInputElement, IInputboxProps>(
  ({ style, type, id, name, children, register, placeholder }, ref: ForwardedRef<HTMLInputElement>) => {
    return (
      <input
        className={style}
        type={type}
        id={id}
        name={name}
        placeholder={placeholder}
        ref={ref}
        {...register}
      />
    );
  }
);

export default Inputbox;
