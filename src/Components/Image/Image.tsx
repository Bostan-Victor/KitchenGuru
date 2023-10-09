import React, { ReactNode } from "react";

interface IImage {
  style?: string;
  url: string;
  children?: ReactNode;
  onMouseEnter?: any;
  onMouseLeave?: any;
  onClick?: any;
}

export default function Image({
  url,
  style,
  children,
  onMouseEnter,
  onMouseLeave,
  onClick,
}: IImage) {
  return (
    <div
      className={style}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onClick={onClick}
    >
      <img src={url} className="rounded-full" />
    </div>
  );
}
