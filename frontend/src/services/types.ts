export type LocationPin = {
  id: number;
  name: string | null;
  address: string | null;
  latitude: number;
  longitude: number;
  source_doc: string | null;
  score: number | null;
  comparison_id: number | null;
  created_at: string;
};

export type PinDetail = {
  score: number | null;
  address: string | null;
  name: string | null;
  source: string | null;
  passes: { label: string; similarity: number }[];
  fails: { label: string; similarity: number }[];
};
