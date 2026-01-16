"use client";

import React, { useEffect } from "react";

const Home = () => {
  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
      console.log(data);
    };
    fetchData();
  }, []);
  return <div>Home</div>;
};

export default Home;
