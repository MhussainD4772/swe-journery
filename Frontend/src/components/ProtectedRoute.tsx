import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { getToken } from "../api";

function ProtectedRoute({ children }: { children: ReactNode }) {
  if (!getToken()) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;
