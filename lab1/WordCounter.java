import java.io.*;
import java.util.*;
import java.util.regex.Pattern;

public class WordCounter {

    public static void main(String[] args) throws FileNotFoundException {
        Counter counter = new Counter();

        try(Scanner file = new Scanner(new File(args[0]))
                              .useDelimiter("(\\p{Punct}|\\p{Space})+")) {

            while (file.hasNext()){
                String word = file.next().toLowerCase();
                counter.addWord(word);
            }

            counter.printOccurences();
        }
    }
}

class Counter {
    private Map<String, Integer> words = new HashMap<>();

    public void addWord(String word) {
        Integer count = words.get(word);
        if(count == null) {
            words.put(word, 1);
        }
        else {
            words.put(word, count + 1);
        }
    } 

    private List<Map.Entry<String, Integer>> sortEntries() {
        List<Map.Entry<String,Integer>> sortedEntries = new ArrayList<>(words.entrySet());

        Collections.sort(sortedEntries, 
            new Comparator<Map.Entry<String,Integer>>() {
                @Override
                public int compare(Map.Entry<String,Integer> e1, Map.Entry<String,Integer> e2) {
                    return e2.getValue().compareTo(e1.getValue());
                }
            }
        );

        return sortedEntries;
    }

    public void printOccurences() {
        for(Map.Entry<String, Integer> entry : sortEntries()) {
            System.out.println(entry.getKey() + " " + entry.getValue());
        }
    }
}