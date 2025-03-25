// app/page.tsx
import React from 'react';

async function fetchData() {
  // Fetch data from your API
  const res = await fetch('http://localhost:8000/openai', { cache: 'no-store' });
  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }
  return res.json();
}

interface ChangeLogItem {
  whats_new: string;
  impact: string;
  changes_description: string;
  other_info: string;
}

interface ChangeLogData {
  new_features: ChangeLogItem[];
  bug_fixes: ChangeLogItem[];
  others: ChangeLogItem[];
}

const NewFeatures = ({ items }: { items: ChangeLogItem[] }) => {
  return (
    <section>
      <h2>New Features</h2>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            <h3>{item.whats_new}</h3>
            <p><strong>Impact:</strong> {item.impact}</p>
            <p><strong>Changes Description:</strong> {item.changes_description}</p>
            {item.other_info && (
              <p><strong>Other Info:</strong> {item.other_info}</p>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
};

const BugFixes = ({ items }: { items: ChangeLogItem[] }) => {
  return (
    <section>
      <h2>Bug Fixes</h2>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            <h3>{item.whats_new}</h3>
            <p><strong>Impact:</strong> {item.impact}</p>
            <p><strong>Changes Description:</strong> {item.changes_description}</p>
            {item.other_info && (
              <p><strong>Other Info:</strong> {item.other_info}</p>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
};

const Others = ({ items }: { items: ChangeLogItem[] }) => {
  return (
    <section>
      <h2>Others</h2>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            <h3>{item.whats_new}</h3>
            <p><strong>Impact:</strong> {item.impact}</p>
            <p><strong>Changes Description:</strong> {item.changes_description}</p>
            {item.other_info && (
              <p><strong>Other Info:</strong> {item.other_info}</p>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
};

export default async function Page() {
  const data = await fetchData();

  return (
    <div>
      <h1>Changelog</h1>
      <NewFeatures items={data.new_features} />
      {data.bug_fixes.length > 0 && <BugFixes items={data.bug_fixes} />}
      <Others items={data.others} />
    </div>
  );
}
