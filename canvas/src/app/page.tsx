import React from 'react';

interface ChangeLogItem {
  whats_new: string;
  impact: string;
  changes_description: string;
  other_info?: string;
}

interface ChangeLogEntry {
  release_name: string;
  new_features: ChangeLogItem[];
  bug_fixes: ChangeLogItem[];
  tests: ChangeLogItem[];
  documentation: ChangeLogItem[];
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
async function fetchData(): Promise<ChangeLogEntry[]> {
  const url = 'https://raw.githubusercontent.com/JaynouOliver/changelog/main/changelog.json';

  try {
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) {
      throw new Error('Failed to fetch changelog data');
    }
    const data: ChangeLogEntry[] = await res.json();
    return data;
  } catch (error) {
    console.error('Error fetching changelog:', error);
    return [];
  }
}

export default async function Page() {
  const entries = await fetchData();

  return (
    <div>
      <h1>Changelog</h1>
      {entries.map((entry, index) => (
        <div key={index} className="changelog-entry">
          <h2 className="release-name">{entry.release_name}</h2>
          {entry.new_features?.length > 0 && <NewFeatures items={entry.new_features} />}
          {entry.bug_fixes?.length > 0 && <BugFixes items={entry.bug_fixes} />}
          {entry.others?.length > 0 && <Others items={entry.others} />}
        </div>
      ))}
    </div>
  );
}
