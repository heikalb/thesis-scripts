import java.util.List;
import zemberek.morphology.TurkishMorphology;
import zemberek.core.logging.Log;
import zemberek.morphology.analysis.SentenceAnalysis;
import zemberek.morphology.analysis.SingleAnalysis;
import zemberek.morphology.analysis.WordAnalysis;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.io.FileWriter;
import java.io.File;

public class ParseMorphemes
{
    public static void main (String[] args) throws IOException
    {
        // Corpus file
        FileReader fileReader = new FileReader("../data/query_results_all_joined_sents_.tsv");
        BufferedReader br = new BufferedReader(fileReader);

        // For Turkish morphological processing
        TurkishMorphology morphology = TurkishMorphology.createWithDefaults();

        //Collect parses
        ArrayList<List> parses = new ArrayList();

        int i = 0;

        // Go through lines in file
        String line;
        while ((line = br.readLine()) != null && i < 5)
        {
            String sentence = line.split("\t")[0];
            List<WordAnalysis> analyses = morphology.analyzeSentence(sentence);
            SentenceAnalysis result = morphology.disambiguate(sentence, analyses);
            parses.add(result.bestAnalysis());

            i++;
        }

        // Save data
        File saveFile = new File("parses.txt");
        FileWriter writer = new FileWriter(saveFile);


        for(List parseList: parses)
        {
            writer.append(parseList.toString() + '\n');
        }

        writer.flush();
        writer.close();
        System.exit(0);
    }
}
