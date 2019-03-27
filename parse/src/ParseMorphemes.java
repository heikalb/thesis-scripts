import java.util.List;
import zemberek.morphology.TurkishMorphology;
import zemberek.morphology.analysis.SentenceAnalysis;
import zemberek.morphology.analysis.WordAnalysis;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
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

        // Go through lines in file
        String line;
        while ((line = br.readLine()) != null)
        {
            String sentence = line.split("\t")[0];
            List<WordAnalysis> analyses = morphology.analyzeSentence(sentence);
            SentenceAnalysis result = morphology.disambiguate(sentence, analyses);
            parses.add(result.bestAnalysis());
        }

        // Save data
        File saveFile = new File("parses_all.txt");
        FileWriter writer = new FileWriter(saveFile);


        for(List parseList: parses)
            writer.append(parseList.toString() + '\n');

        writer.flush();
        writer.close();
        System.exit(0);
    }
}
