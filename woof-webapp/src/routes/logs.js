


import { NavLink, Outlet } from "react-router-dom";
import { getInvoices } from "../data";

export default function Logs() {
  let invoices = getInvoices();
  return (
    <div style={{ display: "flex" }}>
      <nav
        style={{
          borderRight: "solid 1px",
          padding: "1rem",
        }}
      >
        {invoices.map((invoice) => (
        //   <Link
        //     style={{ display: "block", margin: "1rem 0" }}
        //     to={`/logs/${invoice.number}`}
        //     key={invoice.number}
        //   >
        //     {invoice.name}
        //   </Link>
        <NavLink
            style={({ isActive }) => {
              return {
                display: "block",
                margin: "1rem 0",
                color: isActive ? "red" : "",
              };
            }}
            to={`/logs/${invoice.number}`}
            key={invoice.number}
          >
            {invoice.name}
          </NavLink>
        ))}
      </nav>
      <Outlet />
    </div>
  );
}
