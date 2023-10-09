import avatar from "../../assets/image 25.png"
import favorite from "../../assets/Favorite.png"
import wlist from "../../assets/Book.png"
import friends from "../../assets/Group.png"
import logout from "../../assets/Sign_out_squre.png"
import settings from "../../assets/Setting_line.png"
import Button from "../Button/Button"
import { Link, useNavigate, useParams } from 'react-router-dom'
import UserInfo from "../Settings/UserInfo"
import Favorite from "../Settings/Favorite"
import History from "../Settings/History"
import Settings from "../Settings/Settings"
import { useState } from "react"

function SettingsBar() {
  const [data, setData] = useState("UserInfo");
  return (
    <div className="flex">
      <div className=" w-1/4 flex flex-col font-main-font text-3xl ml-[5%] mt-[7%]">
        <ul className="inline-flex">
          <li>
            <div>
              <div className=" absolute h-[70%] w-[10px] rounded-full bg-ECF0F1 ml-[13%] mt-[0%]"></div>
            </div>
          </li>
      <li>
        <div>
          <ul className="mt-2 space-y-24  ">
            <li><span className="ml-[2.5%]">User profile</span></li>
            <li><div>
                <ul className="mt-2 space-y-8 align-middle">
                  <li className="flex items-center align-middle"><img src={avatar} className="w-[50px]" alt="Avatar"/><span className="mt-[0.5%] ml-[1%]"><Button onClick={()=>setData("UserInfo")}>User info</Button></span></li>
                  <li className="flex items-center align-middle"><img src={favorite} className="w-[50px]" alt="Favorite"/> <span className="mt-[0.5%] ml-[1%]"><Button onClick={()=>setData("Favorites")}>Favorites</Button></span></li>
                  <li className="flex items-center align-middle"><img src={wlist} className="w-[50px]" alt="Watch"/> <span className="mt-[0.5%] ml-[1%]"><Button onClick={()=>setData("History")}>History</Button></span></li>
                  <li className="flex items-center align-middle"><img src={settings} className="w-[50px]" alt="Settings"/> <span className="mt-[0.5%] ml-[1%]"><Button onClick={()=>setData("Settings")}>Settings</Button></span></li>
                </ul>
            </div></li>
            <li className="flex items-center align-middle"><img src={logout} className="w-[60px]" alt="Settings"/> <span className=" ml-[1%]">Log Out</span></li>
        </ul>
      </div></li>
    </ul>
</div>
{data === "UserInfo" && <UserInfo />}
{data === "Favorites" && <Favorite />}
{data === "History" && <History />}
{data === "Settings" && <Settings />}
</div>
  );  
}
export default SettingsBar;