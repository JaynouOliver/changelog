// app/page.tsx
import React from 'react';

async function fetchData() {
  // Fetch data from your API
  const res = await fetch('http://localhost:8000/openai', { cache: 'no-store' }); // Use 'no-store' for fresh data on every request
  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }
  return res.json();
}

export default async function Page() {
  const data = await fetchData();

  return (
    <div>
      <h1></h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
