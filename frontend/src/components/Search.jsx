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

export function Search() {
  return (
    <Dialog>
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
          />
        </div>
        <DialogFooter>
          <Button type="submit">Search</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
