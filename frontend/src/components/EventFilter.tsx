import React from 'react';

interface EventFilterProps {
  categories: string[];
  selectedCategory: string | null;
  onCategoryChange: (category: string | null) => void;
}

export const EventFilter: React.FC<EventFilterProps> = ({
  categories,
  selectedCategory,
  onCategoryChange,
}) => {
  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-2">
      <button
        onClick={() => onCategoryChange(null)}
        className={`px-3 py-1.5 rounded-sm border transition-colors whitespace-nowrap ${
          selectedCategory === null
            ? 'bg-primary/20 border-primary text-primary'
            : 'bg-black/50 border-white/10 text-white/70 hover:border-primary/50'
        }`}
      >
        All Categories
      </button>
      
      {categories.map((category) => (
        <button
          key={category}
          onClick={() => onCategoryChange(category)}
          className={`px-3 py-1.5 rounded-sm border transition-colors whitespace-nowrap ${
            selectedCategory === category
              ? 'bg-primary/20 border-primary text-primary'
              : 'bg-black/50 border-white/10 text-white/70 hover:border-primary/50'
          }`}
        >
          {category}
        </button>
      ))}
    </div>
  );
}; 