import React from 'react';

interface ChangeLogItem {
  whats_new: string;
  impact: string;
  changes_description: string;
  other_info?: string;
}

interface ReleaseBlock {
  release_name: string;
  new_features: ChangeLogItem[];
  bug_fixes: ChangeLogItem[];
  tests?: ChangeLogItem[];
  documentation?: ChangeLogItem[];
  others: ChangeLogItem[];
}

// Components for rendering different sections
const NewFeatures = ({ items }: { items: ChangeLogItem[] }) => (
  <section className="mt-6">
    <h2 className="text-xl font-semibold mb-4">New Features</h2>
    <ul className="space-y-6">
      {items.map((item, index) => (
        <li key={index} className="space-y-2">
          <p className="text-lg font-medium">{item.whats_new}</p>
          <p className="text-gray-600 dark:text-gray-300">{item.impact}</p>
          <p className="text-gray-500 dark:text-gray-400 text-sm">{item.changes_description}</p>
          {item.other_info && (
            <p className="text-gray-400 dark:text-gray-500 text-sm">{item.other_info}</p>
          )}
        </li>
      ))}
    </ul>
  </section>
);

const BugFixes = ({ items }: { items: ChangeLogItem[] }) => (
  <section className="mt-6">
    <h2 className="text-xl font-semibold mb-4">Bug Fixes</h2>
    <ul className="space-y-6">
      {items.map((item, index) => (
        <li key={index} className="space-y-2">
          <p className="text-lg font-medium">{item.whats_new}</p>
          <p className="text-gray-600 dark:text-gray-300">{item.impact}</p>
          <p className="text-gray-500 dark:text-gray-400 text-sm">{item.changes_description}</p>
          {item.other_info && (
            <p className="text-gray-400 dark:text-gray-500 text-sm">{item.other_info}</p>
          )}
        </li>
      ))}
    </ul>
  </section>
);

const Tests = ({ items }: { items: ChangeLogItem[] }) => (
  <section className="mt-6">
    <h2 className="text-xl font-semibold mb-4">Tests</h2>
    <ul className="space-y-6">
      {items.map((item, index) => (
        <li key={index} className="space-y-2">
          <p className="text-lg font-medium">{item.whats_new}</p>
          <p className="text-gray-600 dark:text-gray-300">{item.impact}</p>
          <p className="text-gray-500 dark:text-gray-400 text-sm">{item.changes_description}</p>
          {item.other_info && (
            <p className="text-gray-400 dark:text-gray-500 text-sm">{item.other_info}</p>
          )}
        </li>
      ))}
    </ul>
  </section>
);

const Documentation = ({ items }: { items: ChangeLogItem[] }) => (
  <section className="mt-6">
    <h2 className="text-xl font-semibold mb-4">Documentation</h2>
    <ul className="space-y-6">
      {items.map((item, index) => (
        <li key={index} className="space-y-2">
          <p className="text-lg font-medium">{item.whats_new}</p>
          <p className="text-gray-600 dark:text-gray-300">{item.impact}</p>
          <p className="text-gray-500 dark:text-gray-400 text-sm">{item.changes_description}</p>
          {item.other_info && (
            <p className="text-gray-400 dark:text-gray-500 text-sm">{item.other_info}</p>
          )}
        </li>
      ))}
    </ul>
  </section>
);

const Others = ({ items }: { items: ChangeLogItem[] }) => (
  <section className="mt-6">
    <h2 className="text-xl font-semibold mb-4">Others</h2>
    <ul className="space-y-6">
      {items.map((item, index) => (
        <li key={index} className="space-y-2">
          <p className="text-lg font-medium">{item.whats_new}</p>
          <p className="text-gray-600 dark:text-gray-300">{item.impact}</p>
          <p className="text-gray-500 dark:text-gray-400 text-sm">{item.changes_description}</p>
          {item.other_info && (
            <p className="text-gray-400 dark:text-gray-500 text-sm">{item.other_info}</p>
          )}
        </li>
      ))}
    </ul>
  </section>
);

const TimelineDot = () => (
  <div className="absolute -left-[7px] top-[24px] w-3 h-3 bg-white dark:bg-black border-4 border-gray-300 dark:border-gray-700 rounded-full" />
);

const ReleaseBlock = ({ release }: { release: ReleaseBlock }) => (
  <div className="relative pl-8 pb-12 border-l border-gradient-l border-gray-300 dark:border-gray-700">
    <TimelineDot />
    <div className="release-block">
      <div className="flex items-center">
        <span className="inline-block px-2 py-1 text-sm font-mono bg-gray-100 dark:bg-gray-800 rounded-md">
          {release.release_name}
        </span>
      </div>
      {release.new_features?.length > 0 && <NewFeatures items={release.new_features} />}
      {release.bug_fixes?.length > 0 && <BugFixes items={release.bug_fixes} />}
      {release.tests && release.tests.length > 0 && <Tests items={release.tests} />}
      {release.documentation && release.documentation.length > 0 && <Documentation items={release.documentation} />}
      {release.others?.length > 0 && <Others items={release.others} />}
    </div>
  </div>
);

// Fetch data from GitHub raw URL using React Server Component
async function fetchData(): Promise<ReleaseBlock[]> {
  const url = 'https://raw.githubusercontent.com/JaynouOliver/changelog/main/changelog.json';

  try {
    const res = await fetch(url, { cache: 'no-store' }); // Disable cache for real-time updates
    if (!res.ok) {
      throw new Error('Failed to fetch changelog data');
    }
    const data: ReleaseBlock[] = await res.json();
    return data;
  } catch (error) {
    console.error('Error fetching changelog:', error);
    return [];
  }
}

export default async function Page() {
  const releases = await fetchData();

  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      <h1 className="text-4xl font-bold mb-12">Changelog</h1>
      <div className="relative">
        {releases.map((release, index) => (
          <ReleaseBlock key={index} release={release} />
        ))}
      </div>
    </div>
  );
}
