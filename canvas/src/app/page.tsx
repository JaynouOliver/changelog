import React from 'react';

interface ChangeLogItem {
  whats_new: string;
  impact: string;
  changes_description: string;
  other_info?: string; // Optional field
}

interface ChangeLogData {
  new_features: ChangeLogItem[];
  bug_fixes: ChangeLogItem[];
  others: ChangeLogItem[];
}

// Components for rendering different sections
const NewFeatures = ({ items }: { items: ChangeLogItem[] }) => (
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

const BugFixes = ({ items }: { items: ChangeLogItem[] }) => (
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

const Others = ({ items }: { items: ChangeLogItem[] }) => (
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

// Fetch data from GitHub raw URL using React Server Component
async function fetchData(): Promise<ChangeLogData> {
  const url = 'https://raw.githubusercontent.com/JaynouOliver/changelog/main/changelog.json';

  try {
    const res = await fetch(url, { cache: 'no-store' }); // Disable cache for real-time updates
    if (!res.ok) {
      throw new Error('Failed to fetch changelog data');
    }
    const data: { new_features: ChangeLogItem[]; bug_fixes: ChangeLogItem[]; others: ChangeLogItem[] }[] = await res.json();

    // Flatten the data into a single ChangeLogData object
    const flattenedData = {
      new_features: data.flatMap(item => item.new_features || []),
      bug_fixes: data.flatMap(item => item.bug_fixes || []),
      others: data.flatMap(item => item.others || []),
    };

    return flattenedData;
  } catch (error) {
    console.error('Error fetching changelog:', error);
    return {
      new_features: [],
      bug_fixes: [],
      others: [],
    };
  }
}

export default async function Page() {
  const data = await fetchData();

  return (
    <div>
      <h1>Changelog</h1>
      {data.new_features?.length > 0 && <NewFeatures items={data.new_features} />}
      {data.bug_fixes?.length > 0 && <BugFixes items={data.bug_fixes} />}
      {data.others?.length > 0 && <Others items={data.others} />}
    </div>
  );
}
