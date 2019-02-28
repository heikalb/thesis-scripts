import java.io.IOException;
import zemberek.morphology.TurkishMorphology;
import zemberek.normalization.TurkishSpellChecker;
import java.io.FileReader;
import java.io.BufferedReader;
import java.util.ArrayList;
import java.util.List;

public class spellcheckTNC{

    public static void main(String[] args) throws IOException
    {
        TurkishMorphology morphology = TurkishMorphology.createWithDefaults();
        TurkishSpellChecker spellChecker = new TurkishSpellChecker(morphology);

        FileReader fileReader = new FileReader("/Users/heikal/Documents/tez_araştırması/scripts/data/all_sents_spellchecked.txt");
        BufferedReader br = new BufferedReader(fileReader);

        String st;
        ArrayList<String> windows = new ArrayList<String>();
        ArrayList<String> correctedWindows = new ArrayList<>();

        while ((st = br.readLine()) != null)
            windows.add(st);

        for(String window: windows)
        {
            String[] wordsInWindow = window.split(" ");
            ArrayList<String> finalWords = new ArrayList<>();

            for (String w: wordsInWindow)
            {
                if (spellChecker.check(w))
                    finalWords.add(w);
                else
                {
                    List<String> corrections = spellChecker.suggestForWord(w);

                    if (corrections.isEmpty())
                        finalWords.add(w);
                    else
                        finalWords.add(corrections.get(0));
                }
            }
            String r = String.join(" ", finalWords);
            System.out.println(window);
            System.out.println(r);
            // correctedWindows.add(String.join(" ", finalWords));
            correctedWindows.add(r);
        }

    }
}
