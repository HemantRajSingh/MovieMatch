import { useMovieContext } from '../context/movieContext';
import { Button } from '../components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../components/ui/dialog';
import { Textarea } from '../components/ui/textarea';
import { useState } from 'react';

export function Search({ dialogState }) {
  const [query, setQuery] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(dialogState);
  const { fetchRecommendations } = useMovieContext();

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
  };

  return (
    <Dialog open={isDialogOpen} onClose={handleCloseDialog}>
      <DialogTrigger asChild>
        <Button>Search</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[625px]">
        <DialogHeader>
          <DialogTitle>
            Enter keywords, phrases, or themes to explore movies
          </DialogTitle>
          <DialogDescription>
            Search for a specific plot, your favorite actor's latest roles, or
            the visionary works of a particular director.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4">
          <Textarea
            placeholder="Enter keywords, phrases, or themes to explore movies with plots that resonate with your interests."
            className="resize-none min-h-[150px]"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <DialogFooter>
          <Button
            type="submit"
            onClick={() =>
              fetchRecommendations(query, {
                onSuccess: (res) => {
                  setIsDialogOpen(false);
                },
              })
            }
          >
            Search
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
