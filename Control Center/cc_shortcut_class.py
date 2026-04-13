from cc_breakdown_dir import check_if_breakdown
from cc_clipboard import check_if_clipboard
from cc_google_search import check_if_google_search

class Shortcut:
    def __init__(self, input_text):
        self.input_text = input_text
        self.text = input_text
        self.path = ""
        self.text_find = ""
      
        self.is_breakdown, self.text,self.text_find = check_if_breakdown(self.text)
        self.is_clipboard, self.text = check_if_clipboard(self.text)
        self.YYMM = input_text[0:4] if input_text[0:4].isdigit() else ""
        self.is_google_search, self.text, self.path = check_if_google_search(self.text)
        
        if not self.is_google_search:
            self.sc2path()
            
    #############################################
    ## Function to convert a shortcut to a path
    #############################################
    def sc2path(self):
        
        file = open(r"Shortcut_List.txt", "r")

        lines_split = []
        for file_line in file:
            lines_split.append(file_line.split(","))
        file.close()

        for line_split in lines_split:
            
            if(len(line_split) != 2):
                continue
            
            shortcut_line_text = line_split[0]
            shortcut_line_path = line_split[1].replace("\n","")
            
            if self.YYMM != "":
                if "YYMM" in shortcut_line_text: 
                    if shortcut_line_text.replace("YYMM", self.YYMM) == self.text:
                        self.path = shortcut_line_path.replace("YYMM", self.YYMM)
                        break
                        
            if self.text == shortcut_line_text:
                self.path = shortcut_line_path
                break