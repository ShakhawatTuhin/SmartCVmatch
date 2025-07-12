export type Job = {
  id: number;
  title: string;
  company: string;
  location: string;
  matchScore: number;
  description: string;
  postedDate: string;
  isRecommended: boolean;
  isSaved: boolean;
  matchDetails?: {
    skillsMatching: string;
    keywordsMatching: string;
    certificatesMatching: string;
  };
  salary: string;
  jobType: string;
  experience: string;
  skills: string[];
}; 